package hello.login.web.video;


import hello.login.domain.video.Video;
import hello.login.domain.video.VideoRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;

import java.io.IOException;
import java.nio.file.Files;
import java.util.List;

@Controller
@RequestMapping("/videos")
@RequiredArgsConstructor
public class VideoController {
    private final VideoRepository videoRepository;


    @GetMapping
    public String videos(Model model) {
        List<Video> videos = videoRepository.findAll();
        model.addAttribute("videos", videos);
        return "videos/videos";
    }

    @GetMapping("/{videoId}")
    public String video(@PathVariable long videoId, Model model) {
        Video video = videoRepository.findById(videoId);
        model.addAttribute("video", video);
        return "videos/video";
    }

    @GetMapping("/{videoId}/play")
    public ResponseEntity<Resource> playVideo(@PathVariable("videoId") long videoId) {
        String videoPath = "static/videos/" + videoId + ".mp4";
        Resource videoResource = new ClassPathResource(videoPath);

        return ResponseEntity.ok()
                .contentType(MediaType.parseMediaType("video/mp4"))
                .body(videoResource);
    }


}
